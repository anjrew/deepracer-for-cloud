# Saving and useing custom images

To save an image example
1. Commit the image so it exists in your local image repository
    ```bash
    docker commit -a "Andrew Johnson <andrewmjohnson549@gmail.com>" -m "Fix the ip address to MinIO and  add 'unique_episode' to function calls for multiple workers" 9d91714ebc3a my-deepracer-analysis:latest
    ```
2. Save to a .tar file for permanent storage:
    ```bash 
    docker save -o ./my-deepracer-analysis.tar my-deepracer-analysis:latest
    ```