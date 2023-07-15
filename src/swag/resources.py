html_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{{ pagename }}</title>
    <link rel="stylesheet" type="text/css" href="/assets/styles.css" />
  </head>
  <body>
    <nav>
      <input type="checkbox" id="menu-toggle" />
      <label for="menu-toggle" class="menu-btn">
        <span class="menu-icon"></span>
      </label>
      <ul class="menu">
        <li><a href="/">Home</a>.</li>
        <li><a href="/posts/">Blog</a>.</li>
      </ul>
    </nav>
    <div class="container">{{ body }}</div>
    <footer>
      <p>This site was made with <a href="https://github.com/peterprescott/simple-swag"><code>swag</code></a>.</p>
    </footer>
    </body>
</html>
"""

example_css = """
/* Reset some default styles for better consistency */
html, body, div, span, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, img, small, strong, b, i, em, sub, sup, strike, del, ins, u, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, figure, footer, header, nav, section {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

/* Global styles */
body {
  font-size: 18px;
  line-height: 1.5;
  color: #333;
  background-color: #f8f8f8;
}

.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 20px;
}

canvas {
  display: block;
  background-color: #A7CCED;
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1;
}

h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

p {
  margin-bottom: 15px;
}

a {
  color: black;
  font-weight: bold;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.circ {
  border-radius: 50%;
}

.greeting {
 display: flex;
 justify-content: center;
 font-size: 48px;
 font-weight: bold;
}

.signup {
 display: flex;
 justify-content: center;
 text-align: center;
 font-size: 32px;
 padding: 10px;
}

.signup-button {
 left: 50%;
 background-color: #304D6D;
 position: absolute;
 left: 50%;
 -ms-transform: translate(-50%, -50%);
 transform: translate(-50%, -50%);
 font-size: 32px;
 padding: 10px;
 border-radius: 10%;
 font-weight: bold;
 color: white;
}

.vertical-center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}

/* Responsive styles */
@media (max-width: 768px) {
  .container {
    padding: 10px;
  }

  h1 {
    font-size: 20px;
  }
}

/* Footer styles */
footer {
  height: 60px;
  background-color: #82A0BC;
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  text-align: center;
}

footer::before {
  content: "";
  display: inline-block;
  height: 100%;
  vertical-align: middle;
}

footer p {
  display: inline-block;
  vertical-align: middle;
}

/* Hamburger menu styles */
nav {
  background-color: #304D6D;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 25px;
  padding: 10px;
}

.menu-btn {
  display: none;
}

.menu-icon {
  display: block;
  width: 30px;
  height: 2px;
  background-color: #fff;
  position: relative;
  top: 7px;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.menu-icon:before,
.menu-icon:after {
  content: '';
  position: absolute;
  width: 30px;
  height: 2px;
  background-color: #fff;
  transition: background-color 0.3s ease;
}

.menu-icon:before {
  top: -8px;
}

.menu-icon:after {
  top: 8px;
}

.menu-btn:hover .menu-icon,
.menu-btn:focus .menu-icon {
  background-color: #ccc;
}

.menu-btn:hover .menu-icon:before,
.menu-btn:focus .menu-icon:before,
.menu-btn:hover .menu-icon:after,
.menu-btn:focus .menu-icon:after {
  background-color: #ccc;
}

.menu {
  display: flex;
  list-style-type: none;
}

.menu li {
  padding: 10px;
}

.menu li a {
  text-decoration: none;
  color: #fff;
  transition: color 0.3s ease;
}

.menu li a:hover,
.menu li a:focus {
  color: #ccc;
}

#menu-toggle {
    display: none;
  }

/* Media query for mobile */
@media (max-width: 768px) {
  .menu-btn {
    display: block;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
    z-index: 1;
  }

  .menu {
    display: none;
    position: absolute;
    top: 40px;
    right: 0;
    background-color: #333;
    width: 150px;
    padding: 10px;
  }

  .menu li {
    padding: 5px 0;
  }

  .menu li a {
    color: #fff;
  }

  #menu-toggle:checked ~ .menu {
    display: block;
  }
}
"""

example_config = """
[site]
  name = "Joe's Blog"

[owner]
  name = 'Joe Bloggs'
  email = 'joe@bloggs.com'

[social]
  github = 'joebloggs'
  linkedin = 'joebloggs'

[avatar]
   seed = 'joebloggs'

[colors]
  palette = 'random'
"""
