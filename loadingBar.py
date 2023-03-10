import time

def update_loading_bar(progress):
    bar_length = 40
    filled_length = int(progress * bar_length)
    empty_length = bar_length - filled_length
    bar_fill = "█"
    bar_empty = "░"
    bar = bar_fill * filled_length + bar_empty * empty_length
    return f"\rLoading... ║ {bar} {progress:.0%} ║"

def loading_bar():
    start_time = time.time()
    end_time = start_time + 40
    
    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        progress = elapsed_time / 40
        typer.echo(update_loading_bar(progress), nl=False)
        time.sleep(0.1)
