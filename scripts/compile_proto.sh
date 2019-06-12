#!/bin/bash
# Requires protobuf compiler (protoc): https://github.com/protocolbuffers/protobuf

protoc --proto_path=../knead/utils/ --python_out=../knead/utils/ ../knead/utils/glyph_batch.proto
