# Diet Optimization with Ortools and Flask

This repository contains a web application that optimizes a diet plan using linear programming with Ortools, and is deployed using Flask. The application allows users to input their daily nutritional requirements and computes the optimal combination of foods to meet these requirements at the minimum cost. The optimization problem is based on the Stigler diet problem.

## Features

- **User-Friendly Interface**: A professional and responsive web interface built with Flask and Bootstrap.
- **Asynchronous Execution**: Uses Celery and Redis for handling long-running optimization tasks asynchronously.
- **Detailed Results**: Displays the optimal food choices and their costs, along with the nutrient amounts and minimum requirements.

## Technologies Used

- **Flask**: For building the web application.
- **Ortools**: For solving the linear programming optimization problem.
- **Celery**: For asynchronous task management.
- **Redis**: As the message broker for Celery.
- **Pandas**: For handling and displaying data in tabular form.

## Getting Started

Follow the instructions in the `README.md` to set up the project locally and deploy it.

## Links

- [Stigler Diet Problem - Wikipedia](https://en.wikipedia.org/wiki/Stigler_diet)
- [Ortools - Google Developers](https://developers.google.com/optimization)

## License

This project is licensed under the MIT License.
