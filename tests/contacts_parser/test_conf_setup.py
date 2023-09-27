from contacts_parser import conf

def test_path_update():
    conf.setup_paths("test_folder/source.csv")
    assert str(conf.src_file_path).endswith("test_folder/source.csv")
    assert str(conf.destination_folder).endswith("/test_folder/dest")