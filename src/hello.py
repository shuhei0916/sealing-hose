from common import validate_system_coherence, validate_timestamp


def print_hello():
    print("hello")
    

def main():
    validate_timestamp()
    # validate_system_coherence()
    print_hello()
    

if __name__ == '__main__':
    main()