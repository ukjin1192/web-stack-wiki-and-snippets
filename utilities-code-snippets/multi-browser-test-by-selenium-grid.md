#### Get Selenium grid

- Visit <a href="http://www.seleniumhq.org/download/" target="_blank">Selenium</a> website
- Download `Selenium Standalone Server`

#### `SeleniumTest.java`

~~~~
import java.net.URL;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Platform;
import org.openqa.selenium.Point;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;

public class SeleniumTest {

	public static void main(String[] args) throws Exception {

		// Set web driver
		String baseURL = 'http://mysite.com';
		String nodeURL = 'http://127.0.0.1:5566/wd/hub';

		DesiredCapabilities capability = DesiredCapabilities.iphone();
		capability.setBrowserName("firefox");
		capability.setPlatform(Platform.VISTA);

		WebDriver driver = new RemoteWebDriver(new URL(nodeURL), capability);
		
		// Wait 3 seconds if element is not loaded yet
		driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

		// Set browser size
		driver.manage().window().setPosition(new Point(0, 0));
		driver.manage().window().setSize(new Dimension(1024, 768));
		
		// Enable native JS command
		JavascriptExecutor jse = (JavascriptExecutor) driver;

		// Test on target site
		driver.get(baseURL + '/');
		jse.executeScript("$('#sample-modal').modal('hide');");
		jse.executeScript("window.scrollTo(0,document.body.scrollHeight);");
		driver.findElement(By.cssSelector('#login')).click();
		driver.findElement(By.cssSelector('#search')).sendKeys('sample keyword');
		driver.findElement(By.xpath("(//button[@type='submit'])[0]")).click();
		driver.quit();
	}
}
~~~~
