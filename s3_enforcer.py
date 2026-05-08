import boto3

print("=" * 55)
print("   S3 SECURITY ENFORCER by papa_jay")
print("=" * 55)

s3 = boto3.client('s3')
buckets = s3.list_buckets()
bucket_list = buckets['Buckets']

print(f"\nScanning {len(bucket_list)} S3 buckets...\n")

issues = 0

for bucket in bucket_list:
    name = bucket['Name']
    print(f"BUCKET: {name}")
    try:
        pab = s3.get_public_access_block(Bucket=name)
        config = pab['PublicAccessBlockConfiguration']
        if not all(config.values()):
            print(f"  WARNING: Public access NOT fully blocked!")
            issues += 1
        else:
            print(f"  OK: Public access blocked")
    except:
        print(f"  WARNING: No public access block!")
        issues += 1
    try:
        s3.get_bucket_encryption(Bucket=name)
        print(f"  OK: Encryption enabled")
    except:
        print(f"  WARNING: No encryption!")
        issues += 1
    print("")

print("=" * 55)
print(f"   SCAN COMPLETE - {issues} issues found")
print("=" * 55)
