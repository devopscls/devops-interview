#!/bin/bash

# Decrypt and source the secrets file
openssl aes-256-cbc -d -salt -in secrets.enc -out secrets.sh
source secrets.sh
rm -f secrets.sh  # Remove the decrypted file after sourcing

# Continue with the rest of your script

# Step 1: Find log files older than 60 days and 2 GB
find $LOG_PATH -type f -size +2G -exec mv {} $ARCHIVE_PATH \;
find $LOG_PATH -type f -mtime +60 -exec mv {} $ARCHIVE_PATH \;

# Step 2: Tar.gz the files
TAR_FILE="$ARCHIVE_PATH/logs_$(date '+%Y%m%d').tar.gz"
tar -czvf $TAR_FILE -C $ARCHIVE_PATH .

# Step 3: Upload the tar.gz file to S3 bucket
aws s3 cp $TAR_FILE s3://$BUCKET_NAME/ --profile $AWS_PROFILE

# Step 4: Confirm upload
aws s3 ls s3://$BUCKET_NAME/ --profile $AWS_PROFILE

# Step 5: Remove the tar.gz file from the local VM
#rm -rf $TAR_FILE

echo "Log archival and upload to S3 completed successfully."

