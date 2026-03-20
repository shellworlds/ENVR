const fs = require("fs");
const path = require("path");

function indexDir(dir) {
  return fs.readdirSync(dir).map((name) => {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    return { name, bytes: st.size, mtime: st.mtime.toISOString() };
  });
}

console.log(JSON.stringify(indexDir(process.argv[2] || "."), null, 2));
