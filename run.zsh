echo $STITCH_CONFIG_FILE | base64 -d > target_config.json
tap-15five --config tap_config.json | target-stitch --config target_config.json
