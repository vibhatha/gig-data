import os

from utils import File, Log, TSVFile

log = Log("build_gig2_custom_ec")

DIR_GIG2 = os.path.join("gig2")
DIR_GIG2_CUSTOM = os.path.join("gig2_custom_ec_only_smaller")

VALID_FIELDS = [
    "entity_id",
    "valid",
    "rejected",
    "polled",
    "electors",
]


def make_dirs():
    if not os.path.exists(DIR_GIG2_CUSTOM):
        os.makedirs(DIR_GIG2_CUSTOM)


def is_valid_ent_id(x: str):
    return x.startswith("EC-") or x == "LK"


def process_file(file_name: str):
    log.info(f"Processing {file_name}")
    file_path = os.path.join(DIR_GIG2, file_name)
    d_list = TSVFile(file_path).read()

    # entity_id	valid	rejected	polled	electors	UNP	SLFP	SLMC	TULF
    new_d_list = []

    # lk_d
    lk_d = [d for d in d_list if d["entity_id"] == "LK"][0]
    lk_party_to_votes = {}
    for k, v in lk_d.items():
        if k in VALID_FIELDS:
            continue
        lk_party_to_votes[k] = int(round(float(v), 0))

    sorted_party_to_votes = dict(
        sorted(
            lk_party_to_votes.items(), key=lambda item: item[1], reverse=True
        )
    )
    total_votes = sum(sorted_party_to_votes.values())
    p_limit = 0.0001
    vote_limit = total_votes * p_limit

    party_list = [
        x[0] for x in sorted_party_to_votes.items() if x[1] > vote_limit
    ]
    log.debug(f"{party_list=}")
    all_valid_fields = VALID_FIELDS + party_list
    for d in d_list:
        entity_id = d["entity_id"]
        if not is_valid_ent_id(entity_id):
            continue

        new_d = {}
        votes_other = 0
        for k, v in d.items():
            if k != "entity_id":
                v = int(round(float(v), 0))
            if k in all_valid_fields:
                new_d[k] = v
            else:
                votes_other += int(round(float(v), 0))

        new_d["__OTHER"] = str(votes_other)

        new_d_list.append(new_d)

    new_file_path = os.path.join(DIR_GIG2_CUSTOM, file_name)
    TSVFile(new_file_path).write(new_d_list)

    # HACK!
    File(new_file_path).write_lines(
        [line for line in File(new_file_path).read_lines() if line.strip()]
    )

    size_k = os.path.getsize(new_file_path) / 1024
    log.info(
        f"Wrote {new_file_path} ({len(new_d_list)} lines, {size_k:.0f} KB)"
    )

    log.info("." * 40)


def main():
    make_dirs()
    for file_name in os.listdir(DIR_GIG2):
        if not file_name.endswith(".tsv"):
            continue
        if file_name.startswith("government-elections"):
            process_file(file_name)


if __name__ == "__main__":
    main()
