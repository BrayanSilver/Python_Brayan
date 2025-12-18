"""
Script de Teste - Verifica se todas as bibliotecas foram instaladas corretamente
"""

print("=" * 60)
print("TESTE DE INSTALACAO - Python_Brayan")
print("=" * 60)
print()

# Testa cada biblioteca
bibliotecas = {
    'psutil': 'Monitor de Sistema',
    'requests': 'Web Scraper, Downloads',
    'beautifulsoup4': 'Web Scraper',
    'pandas': 'Gerador de Relatorios',
    'openpyxl': 'Gerador de Relatorios (Excel)',
    'win10toast': 'Notificacoes Desktop'
}

print("Verificando bibliotecas instaladas...")
print("-" * 60)

todas_ok = True

for lib, descricao in bibliotecas.items():
    try:
        if lib == 'beautifulsoup4':
            import bs4
            print(f"OK - {lib:20} ({descricao})")
        elif lib == 'win10toast':
            import win10toast
            print(f"OK - {lib:20} ({descricao})")
        else:
            __import__(lib)
            print(f"OK - {lib:20} ({descricao})")
    except ImportError as e:
        print(f"ERRO - {lib:20} NAO INSTALADO!")
        print(f"       Execute: pip install {lib}")
        todas_ok = False

print("-" * 60)

if todas_ok:
    print()
    print("SUCESSO! Todas as bibliotecas estao instaladas!")
    print()
    print("Voce pode executar qualquer projeto agora:")
    print("  - cd monitor_sistema && python monitor.py")
    print("  - cd automacao_downloads && python download_manager.py")
    print("  - cd notificacoes_desktop && python notifier.py")
    print("  - etc...")
    print()
    print("Ou use o script testar_projetos.bat para um menu interativo!")
else:
    print()
    print("ATENCAO! Algumas bibliotecas nao foram instaladas.")
    print("Execute: pip install psutil requests beautifulsoup4 pandas openpyxl win10toast")

print("=" * 60)
