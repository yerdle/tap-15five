
import os
import json
import singer
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

from tap_15five.request_data import tap_data
from tap_15five.request_data import sample_data

REQUIRED_CONFIG_KEYS = ["start_date", "access_token", "user_agent"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():

        # TODO: populate any metadata and stream's key properties here..
        mock_mdata = metadata.get_standard_metadata(schema.to_dict())
        metadata.write(metadata.to_map(mock_mdata), (), "selected", True)
        mock_keyprops = ['id']

        stream_metadata = mock_mdata
        key_properties = mock_keyprops
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def sync(config, state, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog

    for stream in catalog.get_selected_streams(state):
        LOGGER.info('Syncing stream: %s', stream.tap_stream_id)

        bookmark_column = stream.replication_key
        is_sorted = True  # TODO: indicate whether data is sorted ascending on bookmark value
        activate_version_ind = True #full table replication of all streams

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties
        )

        columns = list(stream.schema.to_dict().get('properties').keys())

        max_bookmark = None
        for row in tap_data(config, stream.tap_stream_id, columns):
            # TODO: place type conversions or transformations here

            # write one or more rows to the stream:
            singer.write_records(stream.tap_stream_id, [row])
            if bookmark_column:
                if is_sorted:
                    # update bookmark to latest value
                    singer.write_state({stream.tap_stream_id: row[bookmark_column]})
                else:
                    # if data unsorted, save max value until end of writes
                    max_bookmark = max(max_bookmark, row[bookmark_column])
        if bookmark_column and not is_sorted:
            singer.write_state({stream.tap_stream_id: max_bookmark})

        if activate_version_ind:
            activate_version = max_bookmark
            activate_version_message = singer.ActivateVersionMessage(
                stream=stream_name,
                version=activate_version)
        else:
            activate_version = None

        if total_records > 0
            # End of Stream: Send Activate Version (if needed)
            if activate_version_ind:
                singer.write_message(activate_version_message)
        else:
            LOGGER.warning('NO NEW DATA FOR STREAM: {}'.format(stream_name))

        LOGGER.info('Synced: {}, total_records: {}'.format(
                        input_stream_id,
                        total_records))
        LOGGER.info('FINISHED Syncing: {}'.format(input_stream_id))

    return


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
