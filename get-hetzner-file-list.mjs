import { S3Client, ListObjectsV2Command } from "@aws-sdk/client-s3";

// Configure S3 client
const s3 = new S3Client({
  region: "fsn1",
  endpoint: "https://fsn1.your-objectstorage.com", 
  credentials: {
    accessKeyId: "KC8VDWT5OVC0NS1Q4754",        //38ECPQ31SHLXNSEHSM30
    secretAccessKey: "yAad5AkIA6396yiBGwoVYKRNKTBQiHDV7CYg9quR",     //MdNhzS5YLgc35C2RF3XOF6DDB6yMBXC4zDnb3LmqaE6CfIgdNR6oT7wQkfSznBXm
  },
});

let timestampIndex = 0;
// Function to parse timestamp from filename
function parseTimestamp(filename) {
  timestampIndex++;
  const regex = /^(\d{4}-\d{2}-\d{2})--(\d{2})-(\d{2})\.mp3$/;
  const match = filename.match(regex);
  if (match) {
    const [_, datePart, hour, minute] = match;
    const timestamp = new Date(`${datePart}T${hour}:${minute}:00.00Z`);
    console.log(timestampIndex, " timestamp : ", timestamp);

    return  timestamp;
  }
  return null;
}

async function getAccurateFileCount(bucketName, prefix = "") {
  let totalFiles = 0;
  let continuationToken = undefined;

  try {
    do {
      const command = new ListObjectsV2Command({
        Bucket: bucketName,
        Prefix: prefix,
        MaxKeys: 1000, // Explicitly setting max keys per request
        ContinuationToken: continuationToken,
      });

      const response = await s3.send(command);

      totalFiles += response.Contents ? response.Contents.length : 0;
      continuationToken = response.IsTruncated ? response.NextContinuationToken : undefined;

    } while (continuationToken);

    console.log(`✅ Accurate total number of files: ${totalFiles}`);
    return totalFiles;

  } catch (error) {
    console.error("Error:", error);
    return 0;
  }
}

// Get files closest to the current time
async function getClosestFiles(bucketName, prefix, numFiles = 3) {

  let ContinuationToken = undefined;

  try {

    let data;
    do {
        data = await s3.send(new ListObjectsV2Command({
        Bucket: bucketName,
        Prefix: prefix,
        ContinuationToken,
      }));

      // totalFiles += data.KeyCount || 0;
      ContinuationToken = data.IsTruncated ? data.NextContinuationToken : null;

    } while (ContinuationToken);

    // const data = await s3.send(new ListObjectsV2Command({
    //   Bucket: bucketName,
    //   Prefix: prefix,
    // }));

    if (!data.Contents || data.Contents.length === 0) {
      console.log("No files found.");
      return [];
    }

    const currentTime = new Date();
    console.log("currentTime:", currentTime);


    // Map files to their timestamps
    const filesWithTimes = data.Contents
      .map(item => {
        const timestamp = parseTimestamp(item.Key.split('/').pop());
        return timestamp ? { key: item.Key, timestamp } : null;
      })
      .filter(Boolean);

    // Sort by closest timestamp to current time
    filesWithTimes.sort((a, b) => 
      Math.abs(a.timestamp - currentTime) - Math.abs(b.timestamp - currentTime)
    );

    // Select closest files
    const closestFiles = filesWithTimes.slice(0, numFiles);

    console.log("Closest files:", closestFiles.map(f => f.key));
    return closestFiles.map(f => f.key);

  } catch (error) {
    console.error("Error:", error);
    return [];
  }
}

// Usage example
getClosestFiles("jpost", "radio-103fm/audio/");
