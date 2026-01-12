from contacts_parser import conf
from contacts_parser.parsers import pandas_toolbox as parser
from contacts_parser.writers import contacts_writer as writer

def run() -> None:
    raw_data = parser.load_dataframe(conf.src_file_path, sep=conf.CSV_SEPARATOR)

    writer.write("no_data", parser.extract_unusable_data(raw_data, conf.EMAIL_COLUMNS))

    parser.clean_dataset(raw_data, conf.EMAIL_COLUMNS)
    clean_data = parser.build_dataset_of_parents(raw_data, conf.PARENT1_COLUMNS, conf.PARENT2_COLUMNS)
    parser.clean_dataset(clean_data, [conf.EMAIL_COLUMNS[0]])

    classes_groups = clean_data.sort_values(["NOM", "PRENOM"]).groupby("DIV.")

    for processing_div, processing_dataset in classes_groups:
        writer.write(processing_div, parser.to_gmail_csv(processing_dataset))

