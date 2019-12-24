from server.Server import Server

if __name__ == '__main__':
    while True:
        try:
            s = Server()
            s.start()
        except OSError as e:
            print("OS: "+str(e))
            break
        except BaseException as e:
            print("[ERROR] {}".format(str(e)))

