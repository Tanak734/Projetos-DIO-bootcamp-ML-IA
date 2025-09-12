import argparse
from agent import generate_tests, save_tests

def read_file(filename):
    """
    Lê o conteúdo de um arquivo
    """
    with open(filename, 'r') as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description='Gera testes unitários para código Python')
    parser.add_argument('filename', help='Nome do arquivo Python para gerar testes')
    
    args = parser.parse_args()
    
    # Lê o código do arquivo
    code = read_file(args.filename)
    
    # Gera os testes
    print("Gerando testes...")
    tests = generate_tests(code)
    
    # Salva os testes em um arquivo
    test_filename = save_tests(tests, args.filename)
    print(f"Testes salvos em {test_filename}")
    
    # Mostra os testes gerados
    print("\nTestes gerados:")
    print("=" * 50)
    print(tests)

if __name__ == "__main__":
    main()