from agent import RequestWatcherAgent
def main():
    rwa = RequestWatcherAgent("../data/request_data.csv","../data/agent_backup.csv")
    rwa.start()
if __name__ == "__main__":
    main()