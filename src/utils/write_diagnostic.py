def write_diagnostic(text):
    with open('./output/diagnostic.txt', mode='a') as f:
        f.write(text)
