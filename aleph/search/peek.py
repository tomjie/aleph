import math
from werkzeug.datastructures import MultiDict

from aleph import authz
from aleph.index import TYPE_DOCUMENT
from aleph.core import get_es, get_es_index
from aleph.model import Collection
from aleph.search.documents import text_query
from aleph.search.fragments import filter_query
from aleph.search.util import parse_filters, add_filter


def round(x, factor):
    rnd = int(math.floor(x / float(factor))) * factor
    return 'More than %s' % format(rnd, '0,.0f')


def format_total(obj):
    total = obj.pop('total', 0)
    if total == 0:
        total = 'No'
    elif total < 15:
        total = 'Some'
    elif total < 100:
        total = round(total, 10)
    elif total < 1000:
        total = round(total, 100)
    else:
        total = round(total, 1000)
    obj['total'] = total
    return obj


def peek_query(args):
    if not isinstance(args, MultiDict):
        args = MultiDict(args)
    text = args.get('q', '').strip()
    q = text_query(text)

    filters = parse_filters(args)
    for entity in args.getlist('entity'):
        filters.append(('entities.id', entity))

    q = filter_query(q, filters, [])
    q = add_filter(q, {
        'not': {
            'terms': {
                'collection_id': authz.collections(authz.READ)
            }
        }
    })
    q = {
        'query': q,
        'size': 0,
        'aggregations': {
            'collections': {
                'terms': {'field': 'collection_id', 'size': 30}
            }
        },
        '_source': False
    }
    # import json
    # print json.dumps(q, indent=2)
    result = get_es().search(index=get_es_index(), body=q,
                             doc_type=TYPE_DOCUMENT)

    aggs = result.get('aggregations', {}).get('collections', {})
    buckets = aggs.get('buckets', [])
    q = Collection.all_by_ids([b['key'] for b in buckets])
    q = q.filter(Collection.creator_id != None)  # noqa
    objs = {o.id: o for o in q.all()}
    roles = {}
    for bucket in buckets:
        collection = objs.get(bucket.get('key'))
        if collection is None or collection.private:
            continue
        if collection.creator_id in roles:
            roles[collection.creator_id]['total'] += bucket.get('doc_count')
        else:
            roles[collection.creator_id] = {
                'name': collection.creator.name,
                'email': collection.creator.email,
                'total': bucket.get('doc_count')
            }

    roles = sorted(roles.values(), key=lambda r: r['total'], reverse=True)
    roles = [format_total(r) for r in roles]
    total = result.get('hits', {}).get('total')
    return format_total({
        'roles': roles,
        'active': total > 0,
        'total': total
    })
