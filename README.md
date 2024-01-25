
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

Create Boto3 Layer:
Important: The following AWS CLI commands work for Linux, Unix, and macOS operating systems. In each command, make sure that you replace boto3-mylayer with your preferred name for the lib folder and Lambda layer.
1. Create a lib folder:
```shell
LIB_DIR=boto3-mylayer/python
mkdir -p $LIB_DIR
```
2. Install the library to LIB_DIR:
```shell
pip3 install boto3 -t $LIB_DIR
```
3. Zip all the dependencies to /tmp/boto3-mylayer.zip:
```shell
cd boto3-mylayer
zip -r /tmp/boto3-mylayer.zip .
```
4. Publish the layer:
```shell
aws lambda publish-layer-version --layer-name boto3-mylayer --zip-file fileb:///tmp/boto3-mylayer.zip
```
The command returns the new layer's Amazon Resource Name (ARN).
Example Lambda layer ARN
```shell
arn:aws:lambda:region:$ACC_ID:layer:boto3-mylayer:1
```
