#!/usr/bin/env python3

def test_separator_detection():
    """Test the separator detection logic"""
    
    test_paths = [
        r'C:\Users\test\file.properties',
        '/mnt/c/Users/test/file.properties', 
        'C:/Users/test/file.properties',
        'testfiles/file.properties',
        r'testfiles\file.properties',
        'file.properties'  # No separator case
    ]
    
    print("Testing separator detection logic:")
    for path in test_paths:
        backslash_pos = path.rfind('\\')
        slash_pos = path.rfind('/')
        lastsepIndex = max(backslash_pos, slash_pos)
        filename = path[lastsepIndex+1:]
        print(f'{path:40} -> {filename}')

if __name__ == '__main__':
    test_separator_detection()
