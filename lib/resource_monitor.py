import psutil
import time
import functools

def resource_monitor(func):
    """
    A decorator to monitor peak CPU usage, peak RAM usage, memory used specifically by the function,
    and elapsed time during the execution of a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Record start time and initial memory
        start_time = time.time()
        initial_ram = psutil.virtual_memory().used / (1024 ** 2)  # Convert bytes to MB

        # Initialize peak usage trackers
        peak_cpu = 0.0
        peak_ram = 0.0

        # Create a callback function to monitor resource usage
        def monitor_resources():
            nonlocal peak_cpu, peak_ram
            while not stop_monitoring:
                current_cpu = psutil.cpu_percent(interval=0.1)
                current_ram = psutil.virtual_memory().used / (1024 ** 2)  # Convert bytes to MB
                peak_cpu = max(peak_cpu, current_cpu)
                peak_ram = max(peak_ram, current_ram)

        # Start monitoring in a separate thread
        import threading
        stop_monitoring = False
        monitor_thread = threading.Thread(target=monitor_resources)
        monitor_thread.start()

        # Execute the wrapped function
        result = func(*args, **kwargs)

        # Stop monitoring and wait for the thread to finish
        stop_monitoring = True
        monitor_thread.join()

        # Record end time and final memory
        end_time = time.time()

        # Calculate metrics
        elapsed_time = end_time - start_time
        peak_ram = peak_ram - initial_ram

        # Print resource usage statistics
        print("")
        print("------------------------------------------------------------")
        print(f"Function: {func.__name__}")
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")
        print(f"Peak CPU Usage: {peak_cpu:.2f}%")
        print(f"Peak RAM Usage: {peak_ram:.2f} MB(for this application)")

        return result

    return wrapper

# Example Usage
if __name__ == "__main__":
    @resource_monitor
    def sample_function():
        total = 0
        for i in range(10**7):  # Adjusted loop size for demonstration
            total += i
        return total

    sample_function()
