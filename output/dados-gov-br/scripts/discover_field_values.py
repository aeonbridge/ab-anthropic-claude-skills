#!/usr/bin/env python3
"""
Script para descobrir valores reais dos campos da API dados.gov.br
Testa os domínios documentados em FIELD-DOMAINS.md

IMPORTANTE: Este script requer acesso via browser devido a restrições da API.
Use o Swagger UI em: https://dados.gov.br/swagger-ui/index.html
"""

import requests
import json
from typing import Dict, List, Any
from collections import Counter

API_BASE_URL = "https://dados.gov.br/dados/api/publico"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJPaEx6RktTZWNUR1c0V25KT1NLbjFuYU5NTWxTSWxEX29RUGxpZHk5NXN3OUYtT2Zadm9sZnVjX0UtdlZyTzRNT2FTcGNHUGNOMzN4VXNpNiIsImlhdCI6MTc0MjI0Njk4N30.LOboeht1ujLjjS3Qsyn3nlGXbguCN4sb2xIsIenK52s"

class FieldDomainDiscovery:
    """
    Classe para descobrir os domínios (valores válidos) de cada campo
    """

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json"
        }
        self.discoveries = {}

    def discover_resource_types(self, datasets: List[Dict]) -> Dict[str, int]:
        """
        Descobre todos os tipos de recursos encontrados
        Valida ENUM: tipo = INVALIDO, DADOS, DOCUMENTACAO, DICIONARIO_DE_DADOS, API, OUTRO
        """
        tipos = []

        for dataset in datasets:
            resources = dataset.get('resources', [])
            for resource in resources:
                tipo = resource.get('tipo')
                if tipo:
                    tipos.append(tipo)

        counter = Counter(tipos)
        return dict(counter)

    def discover_formats(self, datasets: List[Dict]) -> Dict[str, int]:
        """
        Descobre todos os formatos de arquivo encontrados
        """
        formats = []

        for dataset in datasets:
            resources = dataset.get('resources', [])
            for resource in resources:
                fmt = resource.get('format')
                if fmt:
                    formats.append(fmt.upper())

        counter = Counter(formats)
        return dict(counter)

    def discover_organizations(self, datasets: List[Dict]) -> Dict[str, Dict]:
        """
        Descobre IDs e nomes de organizações
        """
        orgs = {}

        for dataset in datasets:
            org = dataset.get('organization', {})
            if org:
                org_id = org.get('id')
                org_name = org.get('name')
                if org_id and org_name:
                    orgs[org_id] = {
                        'name': org_name,
                        'datasets_count': org.get('quantidadeConjuntoDadosAbertos', 0)
                    }

        return orgs

    def discover_tags(self, datasets: List[Dict]) -> Dict[str, int]:
        """
        Descobre todas as tags usadas
        """
        tags = []

        for dataset in datasets:
            dataset_tags = dataset.get('tags', [])
            for tag in dataset_tags:
                tag_name = tag.get('name')
                if tag_name:
                    tags.append(tag_name)

        counter = Counter(tags)
        return dict(counter)

    def analyze_field_constraints(self, datasets: List[Dict]) -> Dict[str, Any]:
        """
        Analisa restrições de campos (min/max length, formatos, etc.)
        """
        constraints = {
            'title_lengths': [],
            'notes_lengths': [],
            'resource_sizes': [],
            'tags_per_dataset': [],
            'resources_per_dataset': []
        }

        for dataset in datasets:
            # Tamanhos de título
            title = dataset.get('title', '')
            if title:
                constraints['title_lengths'].append(len(title))

            # Tamanhos de notas/descrição
            notes = dataset.get('notes', '')
            if notes:
                constraints['notes_lengths'].append(len(notes))

            # Número de tags
            tags = dataset.get('tags', [])
            constraints['tags_per_dataset'].append(len(tags))

            # Número de recursos
            resources = dataset.get('resources', [])
            constraints['resources_per_dataset'].append(len(resources))

            # Tamanhos de recursos
            for resource in resources:
                size = resource.get('size')
                if size:
                    constraints['resource_sizes'].append(size)

        # Calcular estatísticas
        stats = {}
        for key, values in constraints.items():
            if values:
                stats[key] = {
                    'min': min(values),
                    'max': max(values),
                    'avg': sum(values) / len(values),
                    'count': len(values)
                }

        return stats

    def print_discoveries(self):
        """Imprime todas as descobertas formatadas"""

        print("\n" + "="*80)
        print("DESCOBERTAS DE DOMÍNIOS DE CAMPOS - dados.gov.br API")
        print("="*80)

        if 'resource_types' in self.discoveries:
            print("\n📦 TIPOS DE RECURSOS (campo: tipo)")
            print("-" * 80)
            for tipo, count in sorted(self.discoveries['resource_types'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {tipo:30} : {count:5} ocorrências")

        if 'formats' in self.discoveries:
            print("\n📄 FORMATOS DE ARQUIVO (campo: format)")
            print("-" * 80)
            top_formats = sorted(self.discoveries['formats'].items(), key=lambda x: x[1], reverse=True)[:20]
            for fmt, count in top_formats:
                print(f"  {fmt:30} : {count:5} ocorrências")

        if 'organizations' in self.discoveries:
            print("\n🏛️  ORGANIZAÇÕES (campo: organization)")
            print("-" * 80)
            top_orgs = sorted(
                self.discoveries['organizations'].items(),
                key=lambda x: x[1].get('datasets_count', 0),
                reverse=True
            )[:10]
            for org_id, org_data in top_orgs:
                print(f"  {org_data['name']:40} : {org_data['datasets_count']:4} datasets")

        if 'tags' in self.discoveries:
            print("\n🏷️  TAGS POPULARES (campo: tags)")
            print("-" * 80)
            top_tags = sorted(self.discoveries['tags'].items(), key=lambda x: x[1], reverse=True)[:20]
            for tag, count in top_tags:
                print(f"  {tag:40} : {count:5} ocorrências")

        if 'field_constraints' in self.discoveries:
            print("\n📏 RESTRIÇÕES DE CAMPOS")
            print("-" * 80)
            for field, stats in self.discoveries['field_constraints'].items():
                print(f"\n  {field}:")
                print(f"    Min: {stats['min']}")
                print(f"    Max: {stats['max']}")
                print(f"    Avg: {stats['avg']:.2f}")
                print(f"    Count: {stats['count']}")

    def save_discoveries(self, filename: str = "../references/discovered-values.json"):
        """Salva descobertas em arquivo JSON"""
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.discoveries, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Descobertas salvas em: {filename}")


def main():
    """
    Função principal

    NOTA: Este script está preparado para processar dados da API,
    mas devido às restrições de acesso (retorna HTML), você precisará:

    1. Usar o Swagger UI para fazer chamadas: https://dados.gov.br/swagger-ui/index.html
    2. Copiar as respostas JSON manualmente
    3. Salvar em um arquivo datasets.json
    4. Executar este script apontando para o arquivo
    """

    print("="*80)
    print("DESCOBRIDOR DE DOMÍNIOS DE CAMPOS - dados.gov.br API")
    print("="*80)
    print("\n⚠️  IMPORTANTE:")
    print("Este script requer dados da API em formato JSON.")
    print("\nOpções para obter os dados:")
    print("1. Use Swagger UI: https://dados.gov.br/swagger-ui/index.html")
    print("2. Execute 'Lista conjuntos de dados' com pagina=1")
    print("3. Copie a resposta JSON")
    print("4. Salve em: ../references/sample-datasets.json")
    print("5. Execute este script novamente")

    # Tentar carregar dados de exemplo
    sample_file = "../references/sample-datasets.json"

    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Verificar formato dos dados
        if isinstance(data, dict) and 'result' in data:
            datasets = data['result'].get('results', [])
        elif isinstance(data, dict) and 'results' in data:
            datasets = data['results']
        elif isinstance(data, list):
            datasets = data
        else:
            print(f"\n❌ Formato de dados não reconhecido em {sample_file}")
            return

        if not datasets:
            print(f"\n❌ Nenhum dataset encontrado em {sample_file}")
            return

        print(f"\n✅ Carregados {len(datasets)} datasets de {sample_file}")

        # Iniciar descoberta
        discovery = FieldDomainDiscovery()

        print("\n🔍 Descobrindo domínios de campos...")

        discovery.discoveries['resource_types'] = discovery.discover_resource_types(datasets)
        discovery.discoveries['formats'] = discovery.discover_formats(datasets)
        discovery.discoveries['organizations'] = discovery.discover_organizations(datasets)
        discovery.discoveries['tags'] = discovery.discover_tags(datasets)
        discovery.discoveries['field_constraints'] = discovery.analyze_field_constraints(datasets)

        # Imprimir e salvar descobertas
        discovery.print_discoveries()
        discovery.save_discoveries()

        print("\n✅ Descoberta completa!")

    except FileNotFoundError:
        print(f"\n⚠️  Arquivo {sample_file} não encontrado.")
        print("\nComo criar o arquivo:")
        print("1. Acesse: https://dados.gov.br/swagger-ui/index.html")
        print("2. Abra: GET /dados/api/publico/conjuntos-dados")
        print("3. Clique 'Try it out'")
        print("4. Defina pagina=1, tamanhoPagina=100")
        print("5. Clique 'Execute'")
        print("6. Copie o Response body (JSON)")
        print(f"7. Salve em: {sample_file}")
        print("8. Execute este script novamente")

    except json.JSONDecodeError as e:
        print(f"\n❌ Erro ao decodificar JSON: {e}")
        print(f"Verifique o formato do arquivo {sample_file}")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()