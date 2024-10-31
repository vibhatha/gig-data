import os

from utils import File, Log, TSVFile

log = Log("build_pd_with_postal")


# id	name	country_id	province_id	district_id	ed_id	pd_id	centroid	population
# EC-01A	Colombo North	LK	LK-1	LK-11	EC-01	EC-01A	[6.962235, 79.86993]	131012

# id	name	country_id	province_id	ed_id	centroid	population
# EC-01	Colombo	LK	LK-1	EC-01	[6.869685, 80.019739]	2323964


if __name__ == "__main__":
    pd_tsv_path = os.path.join("ents", "pd.tsv")
    pd_d_list = TSVFile(pd_tsv_path).read()
    pd_with_postal_d_list = pd_d_list

    # Add Postal PDs
    ed_tsv_path = os.path.join("ents", "ed.tsv")
    ed_d_list = TSVFile(ed_tsv_path).read()

    for ed_d in ed_d_list:
        pd_id = ed_d["id"] + "P"
        pd_d = dict(
            id=pd_id,
            name="Postal " + ed_d["name"],
            country_id=ed_d["country_id"],
            province_id=ed_d["province_id"],
            district_id="-",
            ed_id=ed_d["id"],
            pd_id=pd_id,
            centroid=ed_d["centroid"],
            population=ed_d["population"],
        )
        pd_with_postal_d_list.append(pd_d)

    pd_with_postal_d_list.sort(key=lambda x: x["id"])

    pd_with_postal_tsv_path = os.path.join("ents", "pd_with_postal.tsv")
    TSVFile(pd_with_postal_tsv_path).write(pd_with_postal_d_list)

    # HACK!
    File(pd_with_postal_tsv_path).write_lines(
        [
            line
            for line in File(pd_with_postal_tsv_path).read_lines()
            if line.strip()
        ]
    )

    log.info(
        f"Wrote {len(pd_with_postal_d_list)} lines to {pd_with_postal_tsv_path}"
    )
