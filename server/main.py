from Server import Server

if __name__ == '__main__':
    try:
        s = Server()
        s.start()
    except BaseException as e:
        print("[ERROR] {}".format(str(e)))

