function pyllCreateList(app, links, host) {
  const list = document.createElement("ul");

  links.forEach(link => {
    const item = document.createElement("li");
    const anchor = document.createElement("a");
    anchor.href = `${host}/${link.path}`;
    anchor.innerHTML = link.name;
    item.appendChild(anchor);
    list.appendChild(item);
  });

  app.appendChild(list);
}


function pyllMountVersionApp(selector, repo, host) {
  const links = [
    {
      "name": "stable",
      "path": "stable/index.html"
    }
  ];
  const app = document.querySelector(selector);

  fetch(`https://api.github.com/repos/${repo}/git/refs/tags`)
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw Error("Could not fetch tags from GitHub.");
      }
    })
    .then(results => {
      let tags = [];
      results.forEach(result => {
        const tag = result.ref.split("/")[2];
        tags.push(tag);
      });
      tags = tags.sort().reverse();
      tags.forEach(tag => {
        links.push({"name": tag, "path": `${tag}/index.html`});
      });
      pyllCreateList(app, links, host);
    })
    .catch((error) => {
      console.error('Error:', error);
      pyllCreateList(app, links, host);
    });
}

