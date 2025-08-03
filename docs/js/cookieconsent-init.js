window.addEventListener("load", function(){
    window.cookieconsent.initialise({
      palette: {
        popup: { background: "#000" },
        button: { background: "#f1d600", text: "#000" }
      },
      theme: "classic",
      position: "bottom",
      content: {
        message: "This website uses cookies to ensure you get the best experience.",
        dismiss: "Got it!",
        link: "Learn more",
        href: "/privacy/"
      }
    });
  });
  