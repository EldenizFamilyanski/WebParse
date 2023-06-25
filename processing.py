from config_names import FILENAME_MAIN, DCT_TASKS
from modules import logger
from openai_util import get_gpt_response


def processing_1(df):
    """Add column 'Symbols_count' to the DataFrame.
    where 'Symbols_count' is the number of symbols in the 'Text' column.
    """
    if 'Symbols_count' in df.columns:
        logger.warning("Column 'Symbols_count' already exists.")
        return df
    else:
        logger.info("Adding column 'Symbols_count' to the DataFrame.")
        df['Symbols_count'] = df['Text'].str.len() + df['Title'].str.len()
        df.to_csv(FILENAME_MAIN, index=False)


def processing_2(df):
    """Add column 'Text' to the DataFrame."""

    length_of_part = 1500
    indices_empty_text = df[df['Text'].isna()].index
    logger.info(f"Found {len(indices_empty_text)} empty texts.")
    limit = 50
    amount_of_changes = 0
    for index, row in df.iterrows():
        logger.info(" - " * 40)
        if amount_of_changes >= limit:
            break
        if index in indices_empty_text:
            continue
        lnk = row['Link_to_product_page']
        original_text = row['Text']
        title = row['Title']
        logger.info(f"Post-processing text for {lnk}")
        logger.info(f"Number of remaining changes: {limit - amount_of_changes}")
        if row['Symbols_count'] > 1500:
            parts = []
            logger.info(f"Text is too long. Splitting into parts of {length_of_part} symbols.")
            for i in range(0, len(original_text), length_of_part):
                parts.append(original_text[i:i + length_of_part])
            logger.info(f"Text was split into {len(parts)} parts.")
            new_text = ''
            for part_index, text_part in enumerate(parts):
                short = get_gpt_response(DCT_TASKS['pre_description'].format(part_index=part_index, title=title),
                                         text_part, lnk)
                new_text += short
                logger.info(f"Part {part_index + 1}/{len(parts)} is done.")
        else:
            new_text = original_text
            logger.info("Text is short. No need to split.")
        df.loc[index, "Text is changed"] = str(True)
        amount_of_changes += 1
        prepared_text = get_gpt_response(DCT_TASKS['description'].format(title=title), new_text, lnk)
        df.loc[index, 'Description'] = prepared_text
        df.to_csv(f"file {index}.csv", index=False)
        logger.info(f"Short text for {lnk} is done.")
        logger.info("-" * 40)
    df.to_csv(FILENAME_MAIN, index=False)
    logger.info("Post-processing is done.")
    return df


def processing_3(df):
    for index, row in df.iterrows():
        sku = row["Link_to_product_page"].split('/')[-1]
        print(sku)
