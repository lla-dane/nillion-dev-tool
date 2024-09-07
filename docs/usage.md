## Usage

To do local installation, you have 3 different options:

### Option 1: Use Docker
To run using docker:
Step 1: Move to correct folder
```
cd nillion-devnet
```
Step 2: Building the containers
```
docker build -t nillion-python-starter .
```
Step 3: Run the Docker Container:
```
docker run -it nillion-python-starter
```

### Option 2: Build Locally
To run locally:

Step 1: Clone the Repository
Step 2: open the nillion-python-starter folder using:
```
cd nillion-python-starter/
```

Step 3: Install Nillion and its dependencies:
```bash
curl https://nilup.nilogy.xyz/install.sh | bash
```
```
nilup install latest 
nilup use latest 
nilup init
```
For telemetry analysis of wattelk address
```
nilup instrumentation enable --wallet <your-eth-wallet-address>
```

Install minimum python version
```
python3 --version
python3 -m pip --version
```

Create and activate virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

Install the requirements from .txt file in root
```
pip install --upgrade -r requirements.txt
```

For compiling the nada file, run this in the same dir as nada.toml
```
nada build
```

Spinning up local devnet 
```
nillion-devnet
```

To run the client-code, go the respective directory and run: 
```
python3 <client-code>.py
```
