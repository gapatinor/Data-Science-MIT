import pylab
import re
import numpy as np

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""
def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    cof=[]
    for deg in degs:
     model_coeff=pylab.polyfit(x,y,int(deg))
     cof.append(model_coeff)
    return cof

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    sum1=((y-estimated)**2).sum()
    sum2=((y-y.mean())**2).sum()
    R2=1-sum1/float(sum2)
    return R2

def evaluate_models_on_training(x, y, models, x_label, y_label, title):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    estY=[]
    for i in range(len(models)):
     estY.append(pylab.polyval(models[i],x))

    pylab.figure()
    pylab.plot(x, y)
    for i in range(len(models)):
     if(i==0): 
       SE=round(se_over_slope(x, y, estY[i], models[i]),3)
       pylab.plot(x,estY[i], label="Mod"+str(i+1)+" SE:"+str(SE))
     else:
       R2=round(r_squared(y, estY[i]),3)
       pylab.plot(x,estY[i], label="Mod"+str(i+1)+" R2:"+str(R2))
    pylab.legend(loc="best")
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    #pl.title(title)
    pylab.savefig(title+".pdf", format='PDF')
    #pylab.show()


def trend_with_data(climate,month,day,city):
  years=range(1961,2009)
  temp=[]
  for year in years:
    temp.append(climate.get_daily_temp(city, month, day, year))

  years=pylab.array(years)
  temp=pylab.array(temp)
  degs=[1,2,3]
  models=generate_models(years, temp, degs)
  evaluate_models_on_training(years,temp,models,"years","T"+str(day)+"-"\
                              +str(month)+"-"+city,"temp_fix_data")


def annual_temp(climate,city):
  years=range(1961,2009)
  temp=[]
  for year in years:
    total_temp=climate.get_yearly_temp(city, year)
    temp.append(total_temp.mean())

  years=pylab.array(years)
  temp=pylab.array(temp)
  degs=[1,2,3]
  models=generate_models(years, temp, degs)
  evaluate_models_on_training(years,temp,models,"years","T mean "+city,"temp_mean")

def annual_temp_cities(climate,cities):
  years=pylab.array(range(1961,2009))
  temp_total=gen_cities_avg(climate,cities,years)

  years=pylab.array(years)
  temp_total=pylab.array(temp_total)
  degs=[1,2,3]
  models=generate_models(years, temp_total, degs)
  evaluate_models_on_training(years,temp_total,models,"years","T mean cities","temp_mean_cities")


def gen_cities_avg(climate, cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    temp_total=[]
    for year in years:
      temp_city=[]
      for city in cities:
        total_temp=climate.get_yearly_temp(city, year)
        temp_city.append(total_temp.mean())
      temp_total.append(pylab.array(temp_city).mean())
    return temp_total

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    k=window_length-1
    ma=[]
    for i in range(len(y)):
      s=0
      count=0
      for j in range(i-k,i+1):
       if(j>=0): 
        s+=y[j]
        count+=1
      s=s/float(count) 
      ma.append(s)
    return pylab.array(ma)

def annual_moving_avg(climate,city):
  years=range(1961,2009)
  temp=[]
  for year in years:
    total_temp=climate.get_yearly_temp(city, year)
    temp.append(total_temp.mean())

  years=pylab.array(years)
  temp=pylab.array(temp)
  t_moving_avg=moving_average(temp, 5)

  degs=[1,2,3]
  models=generate_models(years,t_moving_avg,degs)
  evaluate_models_on_testing(years,t_moving_avg,models,"years",\
                              "T moving avg "+city,"temp_moving_avg") 

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    RMSE=(((y-estimated)**2).sum())/float(len(y))
    return RMSE

def evaluate_models_on_testing(x, y, models,x_label, y_label, title):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    estY=[]
    for i in range(len(models)):
     estY.append(pylab.polyval(models[i],x))

    pylab.figure()
    pylab.plot(x, y)
    
    for i in range(len(models)):
      RMSE=round(rmse(y, estY),3)
      pylab.plot(x,estY[i],label="Deg"+str(i+1)+" RMSE:"+str(RMSE))
    pylab.legend(loc="best")
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    #pl.title(title)
    pylab.savefig(title+".pdf", format='PDF')
    #pylab.show()
    pylab.close()
 
def predicting_results(climate,city):
  years=range(1961,1990)
  temp=[]
  for year in years:
    total_temp=climate.get_yearly_temp(city, year)
    temp.append(total_temp.mean())

  years=pylab.array(years)
  temp=pylab.array(temp)
  t_moving_avg=moving_average(temp, 5)

  degs=[1,2,3]
  models=generate_models(years,t_moving_avg,degs)
  evaluate_models_on_training(years,t_moving_avg,models,"years",\
                              "T moving avg "+city,"temp_moving_avg_training") 

  years_test=range(1990,2015)
  temp_test=[]
  for year in years_test:
    total_temp_test=climate.get_yearly_temp(city, year)
    temp_test.append(total_temp_test.mean())

  years_test=pylab.array(years_test)
  temp_test=pylab.array(temp_test)
  t_moving_avg_test=moving_average(temp_test, 5)
  evaluate_models_on_testing(years_test,t_moving_avg_test,models,"years",\
                              "T moving avg "+city,"temp_moving_avg_test") 

def gen_std_devs(climate, cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    temp_std=[]
    for year in years:
      temp_city=[]
      for city in cities:
        total_temp=climate.get_yearly_temp(city, year)
        temp_city.append(total_temp.mean()) 
      temp_std.append(np.std(pylab.array(temp_city)))
    temp_std=pylab.array(temp_std)
    return temp_std

C=Climate("data.csv")

trend_with_data(C,1,10,"NEW YORK")
annual_temp(C,"NEW YORK")
annual_temp_cities(C,CITIES)
annual_moving_avg(C,"NEW YORK")
predicting_results(C,"NEW YORK")

years=range(1961,2015)
years=pylab.array(years)
STD=gen_std_devs(C,CITIES,years)
degs=[1]
models=generate_models(years, STD, degs)
evaluate_models_on_training(years, STD, models,"years","std", "std_cities")




