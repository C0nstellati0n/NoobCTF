# rolling in the mud

[Problem](https://github.com/uclaacm/lactf-archive/tree/main/2023/crypto/rolling-in-the-mud)

The challenge gives a picture. It looks like [Pigpen cipher](https://en.wikipedia.org/wiki/Pigpen_cipher). Pigpen cipher is a substitution cipher, which makes it very strange: why does the flag start with "."? Then look at the end of the picture. 5 characters correspond exactly to the length of the flag prefix. It appears that the entire picture has been flipped. I chose to use [Photopea](https://www.photopea.com/) to flip the picture back, and then [decode](https://www.dcode.fr/pigpen-cipher) it to get the flag. 

## Flag
> lactf{rolling_and_rolling_and_rolling_until_the_pigs_go_home}