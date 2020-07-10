# mnist-testbook

---

## Setup repo for docs site

1. Create an ssh key-pair.  Open <a href="https://8gwifi.org/sshfunctions.jsp" target="_blank">this utility</a>. Select: `RSA` and `4096` and leave `Passphrase` blank.  Click the blue button `Generate-SSH-Keys`.

2. Navigate to `https://github.com/YOUR_ORG/YOUR_REPO/settings/secrets` and click `Add a new secret`.  Copy and paste the **Private Key** into the `Value` field. This includes the "---BEGIN RSA PRIVATE KEY---" and "--END RSA PRIVATE KEY---" portions. In the `Name` field, name the secret `SSH_DEPLOY_KEY`.  

3. Navigate to `https://github.com/YOUR_ORG/YOUR_REPO/settings/keys` and click the `Add deploy key` button.  Paste your **Public Key** from step 1 into the `Key` box.  In the `Title`, name the key anything you want, for example `fastpages-key`.  Finally, **make sure you click the checkbox next to `Allow write access`** (pictured below), and click `Add key` to save the key.

![](https://raw.githubusercontent.com/fastai/fastpages/master/_fastpages_docs/_checkbox.png)
