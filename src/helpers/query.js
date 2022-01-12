import http from "../http-common";

async function query(sql) {
    let ret;
    await http
        .get("/trash", { params: { q: sql } })
        .then((response) => (ret = response.data))
        .catch((e) => {
            console.log(e);
            ret = null;
        });
    return ret;
}

export default query;
