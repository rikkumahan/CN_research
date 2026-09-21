# Raw Dataset Folder

Please paste your transferred dataset files here from your SSD:

- **ISCX VPN/non-VPN 2016**: Paste either `.pcap` files or `.csv` files into `data/raw/iscx/`
- **USTC-TFC 2016**: Paste either `.pcap` files or `.csv` files into `data/raw/ustc/`

Once copied, run:
```bash
uv run python src/dataset_loader.py
```
This will automatically parse all PCAPs or CSVs, extract the 8 flow features, and output clean datasets into `data/processed/`.

