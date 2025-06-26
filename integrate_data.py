#!/usr/bin/env python3
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataIntegrator:
    def __init__(self):
        self.raw_dir = Path('data/raw')
        self.processed_dir = Path('data/processed')
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self):
        """Load the most recent data files for each source"""
        data = {}
        
        # Load SIAFI data
        siafi_files = list(self.raw_dir.glob('siafi_*.csv'))
        if siafi_files:
            latest_siafi = max(siafi_files, key=lambda x: x.stat().st_mtime)
            data['siafi'] = pd.read_csv(latest_siafi)
            
        # Load Compras data
        compras_files = list(self.raw_dir.glob('contratos_*.csv'))
        if compras_files:
            latest_compras = max(compras_files, key=lambda x: x.stat().st_mtime)
            data['compras'] = pd.read_csv(latest_compras)
            
        # Load TransfereGov data
        transfere_files = list(self.raw_dir.glob('convenios_*.csv'))
        if transfere_files:
            latest_transfere = max(transfere_files, key=lambda x: x.stat().st_mtime)
            data['transferegov'] = pd.read_csv(latest_transfere)
            
        return data

    def clean_data(self, data):
        """Clean and prepare data for integration"""
        cleaned = {}
        
        for source, df in data.items():
            # Convert column names to lowercase and replace spaces
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            
            # Handle specific cleaning based on source
            if source == 'siafi':
                if 'codigo_ug' in df.columns:
                    df['codigo_ug'] = df['codigo_ug'].astype(str)
            elif source == 'compras':
                if 'uasg' in df.columns:
                    df['uasg'] = df['uasg'].astype(str)
            
            cleaned[source] = df
            
        return cleaned

    def integrate_data(self, cleaned_data):
        """Integrate data using key fields"""
        # Start with SIAFI data if available
        if 'siafi' in cleaned_data:
            integrated = cleaned_data['siafi']
        else:
            return None
            
        # Join with Compras data
        if 'compras' in cleaned_data:
            integrated = pd.merge(
                integrated,
                cleaned_data['compras'],
                left_on='codigo_ug',
                right_on='uasg',
                how='outer',
                suffixes=('_siafi', '_compras')
            )
            
        # Join with TransfereGov data
        if 'transferegov' in cleaned_data:
            integrated = pd.merge(
                integrated,
                cleaned_data['transferegov'],
                on='codigo_siafi',
                how='outer',
                suffixes=('', '_transferegov')
            )
            
        return integrated

    def generate_summary(self, data, integrated):
        """Generate a summary of the integration process"""
        summary = []
        summary.append("=== Resumo da Integração de Dados ===\n")
        
        # Source data statistics
        for source, df in data.items():
            summary.append(f"{source.upper()}:")
            summary.append(f"- Registros: {len(df)}")
            summary.append(f"- Colunas: {len(df.columns)}")
            summary.append("")
            
        # Integration statistics
        if integrated is not None:
            summary.append("DADOS INTEGRADOS:")
            summary.append(f"- Total de registros: {len(integrated)}")
            summary.append(f"- Total de colunas: {len(integrated.columns)}")
            
            # Missing data analysis
            for col in integrated.columns:
                missing = integrated[col].isna().sum()
                if missing > 0:
                    pct = (missing / len(integrated)) * 100
                    summary.append(f"- Campo {col}: {missing} valores faltantes ({pct:.1f}%)")
                    
        return "\n".join(summary)

def main():
    integrator = DataIntegrator()
    
    # Load data
    data = integrator.load_data()
    if not data:
        logger.error("No data files found to process")
        return
        
    # Clean data
    cleaned_data = integrator.clean_data(data)
    
    # Integrate data
    integrated = integrator.integrate_data(cleaned_data)
    
    if integrated is not None:
        # Save integrated data
        output_file = integrator.processed_dir / 'integrated_poc_data.csv'
        integrated.to_csv(output_file, index=False)
        logger.info(f"Saved integrated data to {output_file}")
        
        # Generate and save summary
        summary = integrator.generate_summary(cleaned_data, integrated)
        summary_file = integrator.processed_dir / 'poc_summary.txt'
        with open(summary_file, 'w') as f:
            f.write(summary)
        logger.info(f"Saved summary to {summary_file}")
    else:
        logger.error("Failed to integrate data")

if __name__ == '__main__':
    main()
