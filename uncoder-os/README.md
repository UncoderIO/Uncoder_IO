## Getting Started

### Prerequisites
Add a .env file to the root of the project with the following variables:
```dotenv
UNCODER_API_BASE_URL=_YOUR_UNCODER_API_DOMEN_
```

### Local Development
Install node.js (v20) and npm. Then, install the dependencies:

```bash
npm install
npm run build
npm run start
```

### Using Docker
```bash
docker build -t uncoder-os .
docker run -it -p 4010:4010 uncoder-os
```

Open [http://localhost:4010](http://localhost:3000) with your browser to see the result.

