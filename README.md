# Tiktok-Live

Tiktok-live is a program for easily creating interactive live sessions by engaging with your virtual keyboard.

⚠️Investigation underway regarding certain error messages. Code is functional but may currently contain multiple bugs.

## Installation

Install the modules using PIP with the following command:
```bash
pip install pyautogui TiktokLive colorama logging pynput
```

## Usage

```python
actions = {
    'example1': lambda: example1('', duration=0.1),
    'exeample2': lambda: example2(''),

}
```
Actions represent the actions that can be sent in the chat.
By default, example1 and 2 are added. Feel free to modify the names as you wish.
Don't forget to put the associated key in the '' zone.


```python
def example1(key, duration):
    try:
        keyboard.press(key)
        time.sleep(duration)
        keyboard.release(key)
    except ValueError as e:
        logging.error(f"Touche non reconnue : {e}")

def example2(key):
    try:
        keyboard.press(key)
        keyboard.release(key)
    except ValueError as e:
        logging.error(f"Touche non reconnue : {e}")

```
These functions represent how the action will take place.
In example 1, the key is pressed and held down, then released with the duration added in the action.
In example 2, the key is pressed and released


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
