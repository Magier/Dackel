# Dackel
<u>D</u>etection <u>A</u>s <u>C</u>ode for <u>K</u>ubernetes <u>E</u>vents and <u>L</u>ogs


![Dackel logo](docs/logo.png) ([source](https://www.flaticon.com/de/kostenloses-icon/hund_4787302))

A Dackel is a German hound bred to find and chase burrow-dwelling animals. It's ideal to send down rabbit holes to surfaces suitable detections.


## Feature (Ideas)

- catalog of malware, lolbins, etc. relevant for K8s security 
- Convert TI blog posts to Sigma/Yara rules
- Setup malware analysis environment
    - Run malicious samples and record all syscalls, K8s Api requests, etc.
    - Classify the observed telemetry 
- use pysigma/ [sigconverter.io](https://sigconverter.io/) to generate K8s specific rules
- use vendor repositories as sources for useful Sigma/Yara rules
- generate (Sigma) correlations from atomic detection rules
- rate the detection rate (F1, confidence, [STP](https://center-for-threat-informed-defense.github.io/summiting-the-pyramid/))
- differenaiate between basic (uninformed) detection rules and threat-/campaign- specific rules?