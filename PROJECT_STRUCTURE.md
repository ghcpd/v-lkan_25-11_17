Enterprise-KG-Eval project structure (tree)

v-lkan_25-11_17/
  entities.json
  relations.json
  documents.txt
  requirements.txt
  Dockerfile
  setup.sh
  run_test.sh
  enterprise_kg_eval/
    __init__.py
    main.py
    config_loader.py
    data_loader.py
    output_writer.py
    schema/
      output_schema.py
    engines/
      __init__.py
      base_engine.py
      regex_engine.py
      llm_engine.py
      ml_engine.py
    pipelines/
      engine_factory.py
      entity_extractor.py
      relation_extractor.py
    tests/
      test_config_loader.py
      test_data_loader.py
      test_regex_engine.py
      test_entity_and_relation_pipeline.py
      test_output_writer.py
    test_report_template.json
    scripts/
      setup.sh
      run_test.sh
  output/
    entities_output.json  # pipeline output
    relations_output.json # pipeline output
