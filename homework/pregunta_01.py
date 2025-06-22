"""
Credit application data cleaning script.
"""

import pandas as pd
import os
from typing import List
from datetime import datetime

def clean_text_column(text: str) -> str:
    """Clean individual text values by removing special characters and standardizing format."""
    if not isinstance(text, str):
        return text
    return text.lower().replace('_', ' ').replace('-', ' ')

def clean_text_cols(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Clean multiple text columns in the dataframe."""
    df = df.copy()
    for col in cols:
        df[col] = df[col].apply(clean_text_column)
    return df

def clean_money_amount(amount: str) -> float:
    """Convert string money amount to float."""
    if not isinstance(amount, str):
        return amount
    return float(amount.replace('$', '').replace(',', '').replace('.00', '').strip())

def parse_date(date_str: str) -> datetime:
    """Parse date string into datetime object."""
    parts = date_str.split('/')
    if len(parts[0]) > 2:  # yyyy/mm/dd format
        year, month, day = parts
    else:  # dd/mm/yyyy format
        day, month, year = parts
    return pd.to_datetime(f"{year}-{month}-{day}")

def save_df(df: pd.DataFrame, output_path: str = 'files/output/solicitudes_de_credito.csv'):
    """Save dataframe to CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=True, sep=';')

def pregunta_01():
    """
    Clean the credit applications data file and save the cleaned version.
    Handles duplicates, missing values, and standardizes data formats.
    """
    # Load data
    df = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';', index_col=0)
    
    # Remove duplicates and missing values
    df.drop_duplicates(keep='first', inplace=True)
    df.dropna(inplace=True)
    
    # Clean text columns
    text_columns = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'línea_credito']
    df = clean_text_cols(df, text_columns)
    
    # Clean monetary values
    df.monto_del_credito = df.monto_del_credito.apply(clean_money_amount)
    
    # Parse dates
    df.fecha_de_beneficio = df.fecha_de_beneficio.apply(parse_date)
    
    # Final duplicate check
    df.drop_duplicates(keep='first', inplace=True)
    
    # Save cleaned data
    save_df(df)
    
    return df

if __name__ == "__main__":
    pregunta_01()