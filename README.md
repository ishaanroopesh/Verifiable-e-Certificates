# Verifiable-e-Certificates

A Django-powered web application designed for instructors and students, enabling the creation and verification of e-certificates through a dedicated URL.

-> The web-app allows students to sign up and register with the site, thereby creating an account using Django's built-in User model

-> The instructor and the student will have different looks to their webpages. (Done by checking the staff status of the account that is logged in)

-> The Instructor has the option to create courses, as well as approve students that have enrolled into the particular courses.

-> The Students have the option to join courses of their choice, and view the certificates issued to them for completing courses approved by the instructor.

-> The nature of the web-app allows the website to be lightweight, as the certificates are not stored as an image, rather they are generated on the spot.

-> The unique code associated with each certificate is also linked with the url for that particular page. Using this method, the validity of the certificate is proved because a 'fake' or an invalid url will not associated with a webpage on the site.

-> The admin capabilities of the instructor, can allow them to perform various other operations, like disapproving requests, deleting courses or students from the platform.
