"""
Export predictions for n8n workflow integration.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List


class N8nExporter:
    """Export predictions formatted for n8n workflows."""
    
    @staticmethod
    def export_json(predictions: pd.DataFrame, output_path: Path) -> Path:
        """
        Export predictions as JSON for n8n.
        
        Args:
            predictions: DataFrame with predictions
            output_path: Path to save JSON file
        
        Returns:
            Path to exported file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to list of dictionaries for n8n
        data = []
        for idx, row in predictions.iterrows():
            item = row.to_dict()
            item['id'] = str(idx)
            data.append(item)
        
        with open(output_path, 'w') as f:
            json.dump({'items': data}, f, indent=2)
        
        return output_path
    
    @staticmethod
    def export_webhook_payload(
        predictions: pd.DataFrame,
        webhook_url: str,
    ) -> Dict:
        """
        Format predictions for webhook payload.
        
        Args:
            predictions: DataFrame with predictions
            webhook_url: Target webhook URL
        
        Returns:
            Formatted payload
        """
        return {
            'webhook_url': webhook_url,
            'timestamp': pd.Timestamp.now().isoformat(),
            'data': predictions.to_dict(orient='records'),
            'count': len(predictions),
        }
    
    @staticmethod
    def create_n8n_workflow_payload(
        predictions: pd.DataFrame,
        workflow_id: str = None,
    ) -> Dict:
        """
        Create payload for n8n workflow.
        
        Args:
            predictions: DataFrame with predictions
            workflow_id: Optional workflow identifier
        
        Returns:
            Formatted payload
        """
        return {
            'workflow_id': workflow_id,
            'timestamp': pd.Timestamp.now().isoformat(),
            'predictions': predictions.to_dict(orient='records'),
            'metadata': {
                'total_records': len(predictions),
                'traits': list(predictions.columns),
            }
        }
