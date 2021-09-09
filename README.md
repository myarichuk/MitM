# ARP Spoofing Experiment
This is a small repository that reproduces a [man-in-the-middle attack](https://en.wikipedia.org/wiki/ARP_spoofing) which uses an ARP protocol to redirect traffic to a proxy.

## How to run
1. Execute **docker compose up** on the *docker-compose.yml* in root folder
2. Attach a console to **mitm** service
3. Execute the script *./mitm/setup_mitm.sh*
4. Start **MITMPROXY** interface by running *mitmproxy -m transparent -s ./mitm/proxy.py*
5. Issue an *HTTP* request to **http://localhost:5555/changekey?newkey=foobar123**
6. The following log entries at **MITMPROXY** interface should appear (switch to log mode by pressing *shift + E*, capital 'e')
