import os

def load_env():
    base_dir = "/".join(os.path.realpath(__file__).split("/")[:-3])
    rt_val = {}
    with open(base_dir + "/.config/.env") as f:
        for line in f:
            if not line.startswith("#"):
                rt_val[line.split("=")[0].strip()] = line.split("=")[1].strip()
    print(rt_val)

if __name__ == "__main__":
    load_env()