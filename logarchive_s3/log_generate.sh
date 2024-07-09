cd /Users/vishal/Desktop/DEVOPS/github_projects/logarchive_s3/logs
export LC_ALL=C
# Function to generate random content of specified size
generate_random_content() {
  head -c $1 /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 80 | head -n $(( $1 / 80 ))
}

# Loop to create 30 log files
for ((i=1; i<=30; i++)); 
do
  filename="testing-$i.log"
  content_size=$((1024 * (1 + $i))) # Ensure each log file is more than 1 MB
  generate_random_content $content_size > "$filename"
done
