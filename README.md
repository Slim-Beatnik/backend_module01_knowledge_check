<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Slim-Beatnik/backend_module01_knowledge_check">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Repair Shop DB</h3>

  <p align="center">
    Blueprint:
Create Blueprint folders for mechanic and service ticket. Each Blueprint folder should have the following:
__init__.py: In this file you initialize the blueprint (don't forget to import the routes into this file after the initialization.)
routes.py: Here is were you create the routes specific to that resource
schemas.py: This is the file where you define the schemas used to serialize and deserialize data for the routes
After initializing the the blueprints register them in your app/__init__.py file, and assign a url prefix. Remember url prefixes should be the plural name of the resource (hint: /mechanics, /service-tickets)

Marshmallow Schemas:
Define basic Schemas for your mechanic and service_ticket resources. Remember you can take advantage of SQLAlchemyAutoSchema to quickly generate the schema based of the model you created for that particular resource.

Routes:

Mechanic: Create full CRUD routes for your mechanic resource, and remember you should have a url_prefix set up so a lot of your route endpoints will be '/'.
POST '/' : Creates a new Mechanic
GET '/': Retrieves all Mechanics
PUT '/<int:id>':  Updates a specific Mechanic 

based on the id passed in through the url.
DELETE '/<int:id': Deletes a specific Mechanic based on the id passed in through the url.
Service_Ticket: Create the following routes to Create service tickets, assign mechanics, remove mechanics, and retrieve all service tickets.
POST '/': Pass in all the required information to create the service_ticket.
PUT '/<ticket_id>/assign-mechanic/<mechanic-id>: Adds a relationship between a service ticket and the mechanics. (Reminder: use your relationship attributes! They allow you the treat the relationship like a list, able to append a Mechanic to the mechanics list).
PUT '/<ticket_id>/remove-mechanic/<mechanic-id>: Removes the relationship from the service ticket and the mechanic.
GET '/': Retrieves all service tickets.
Testing and Postman Collections:
As you continue to build new endpoints, you should be testing each endpoint in Postman to ensure functionality. 

Create a Postman collection to store all of these endpoint tests, export the collection and include it with your work. 

If you are unsure how to create and export a Postman collect watch the video linked below.

Presenting
All students who joined Coding Temple February and onward need to present there project either on Thursdays or Friday live sessions, or you can schedule a 1-on-1 with Dylan to present.
For Pre-February students you are still encouraged to present as it is a great way to build you Tech-Communication skills which are a must.
Submitting:
For this assignment and all following, please push your work to github, and submit the link to the github repository.
    <br />
    <a href="https://github.com/Slim-Beatnik/backend_module01_knowledge_check"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Slim-Beatnik/backend_module01_knowledge_check">View Demo</a>
    &middot;
    <a href="https://github.com/Slim-Beatnik/backend_module01_knowledge_check/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Slim-Beatnik/backend_module01_knowledge_check/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Python, MySQL workbench and server, Postman.
Implimented: SQLAlchemy, Flask, Marshmallow

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/Slim-Beatnik/backend_module01_knowledge_check.git
   ```
2. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin Slim-Beatnik/backend_module01_knowledge_check
   git remote -v # confirm the changes
   ```
3. Create a virtual environment
   ```sh
   python -m venv venv
   python3 -m venv venv
   ```
4. Activate the virtual environment
   ```sh
   venv\\Scripts\\Activate
   source venv/bin/activate
   ```
5. Install dependencies:
  pip: ```sh
    pip install -r requirements.txt
  ```
  uv: ```sh
        uv sync
      ```

  then use uv run app.py
6. Bonus ********
  if you're using uv, check out ruff
  Corey Shafer Youtube video: https://www.youtube.com/watch?v=828S-DMQog8

7. Verify paths in Postman:
  import kh-ct-backend-module01_knowledge_check-repairshop_db.postman_collection.json
  You can then run all, or split up your run by folder.
  There is a main folder for creation:
  C___
  And another folder for read, update and delete:
  _RUD


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Slim-Beatnik/backend_module01_knowledge_check/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/Slim-Beatnik/backend_module01_knowledge_check/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Slim-Beatnik/backend_module01_knowledge_check" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - totem64@gmail.com.com

Project Link: [https://github.com/Slim-Beatnik/backend_module01_knowledge_check](https://github.com/Slim-Beatnik/backend_module01_knowledge_check)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Slim-Beatnik/backend_module01_knowledge_check.svg?style=for-the-badge
[contributors-url]: https://github.com/Slim-Beatnik/backend_module01_knowledge_check/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Slim-Beatnik/backend_module01_knowledge_check.svg?style=for-the-badge
[forks-url]: https://github.com/Slim-Beatnik/backend_module01_knowledge_check/network/members
[stars-shield]: https://img.shields.io/github/stars/Slim-Beatnik/backend_module01_knowledge_check.svg?style=for-the-badge
[stars-url]: https://github.com/Slim-Beatnik/backend_module01_knowledge_check/stargazers
[issues-shield]: https://img.shields.io/github/issues/Slim-Beatnik/backend_module01_knowledge_check.svg?style=for-the-badge
[issues-url]: https://github.com/Slim-Beatnik/backend_module01_knowledge_check/issues
[license-shield]: https://img.shields.io/github/license/Slim-Beatnik/backend_module01_knowledge_check.svg?style=for-the-badge
[license-url]: https://github.com/Slim-Beatnik/backend_module01_knowledge_check/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/3dkylehill
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
