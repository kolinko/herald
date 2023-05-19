# Work in Progress

> If you have any queries, feel free to drop me an email at [kolinko@gmail.com](mailto:kolinko@gmail.com)

---

## Running the Application

To run this application, use the following command:

```bash
python3 index.py
```

## Installation

Please follow the steps below to install and setup this application.

### Step 1: Obtain OpenAI GPT-4 API access

To use this application, you will need access to the OpenAI GPT-4 API. If you don't have access yet, you can get it [here](https://openai.com).

### Step 2: Install Redis

This application uses Redis for caching websites and AI queries. To install Redis, follow the instructions provided in the official [Getting Started guide](https://redis.io/docs/getting-started/). 

If for some reason you can't or don't want to use Redis, you can remove the references to it from `common.py`. The application should still work without it, but might be slower at times.

### Step 3: Install Python Requirements

Here are the Python requirements that need to be installed:

- `redis`
- `openai`
- `tqdm`

You can install them by running the following command:

```bash
pip install redis openai tqdm
```

There might be other required packages as well. If you encounter any issues, don't hesitate to ask ChatGPT for help.

---

Looking forward to your contributions! Enjoy coding!
