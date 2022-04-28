import os
import psycopg2
from flask import Flask,render_template,request,redirect,url_for

app=Flask(__name__)

def get_db_connection():
	conn=psycopg2.connect(
	host="localhost",
	database="project",
	user="postgres",
	password="260402"
	# port=5433
)
	return conn


# def get_db_connection():
# 	conn=psycopg2.connect(
# 	host="10.17.50.36",
# 	database="group_43",
# 	user="group_43",
# 	password="GvJ145eOKxO6T",
# 	port=5432
# )
# 	return conn


@app.route('/')
def main_page():
	return render_template('main.html')


@app.route('/firepower')
def get_rankings():
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"SELECT fire_power_rank,country_name FROM country ORDER BY fire_power_rank;"
		)
	countryname=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('firepower.html',title="Fire Power Rankings" ,L=countryname)


@app.route('/army')
def get_army_details():
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"""
		SELECT country_name,combat_tanks,armored_fighters,self_propelled_artillery,towered_artillery,rocket_projectors
		FROM country,army
		WHERE army.army_id=country.army_id
		"""
		)
	army_table=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('army.html',title="Army Details",L=army_table)



@app.route('/navy')
def get_navy_details():
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"""
		SELECT country_name,naval_assets,aircraft_carriers,frigates,destroyers,corvettes,submarines,patrol_crafts,warfare_vessels
		FROM country,navy
		WHERE navy.navy_id=country.army_id
		"""
		)

	countryname=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('navy.html', title="Navy Details",L=countryname)



@app.route('/airforce')
def get_airpower():
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"""
		SELECT country_name,aircraft_rank,aircrafts,fighter_aircrafts,attack_aircrafts,transport_aircrafts,trainer_aircrafts,helicopters,attack_helicopters
		FROM country,airforce
		WHERE country.airforce_id=airforce.airforce_id;
		"""
		)
	countryname=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('airforce.html',title="Airforce Details",L=countryname)



@app.route('/country_details')
def get_countrydetails():
	conn=get_db_connection()
	cur=conn.cursor()
	query='''
	SELECT country_name,iso3,iso2,capital,currency,region,subregion,population,land_area,GDP,fire_power_rank 
	FROM country,economy,geography,manpower 
	WHERE country.economy_id=economy.economy_id AND country.geography_id=geography.geography_id AND 
	country.manpower_id=manpower.manpower_id
	'''
	cur.execute(query)
	countryname=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('country_details.html',title="Countries and Their Statistics",L=countryname)


@app.route('/economy')
def get_economy():
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"""
		SELECT country_name,defence_budget,external_debt,forex,purchasing_power,gdp
		FROM country,economy
		WHERE country.economy_id=economy.economy_id
		"""
		)
	countryname=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('economy.html',title="Economic Details",L=countryname)

@app.route('/geography')
def get_geography():
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"""
		SELECT country_name,land_area,coastline_length,shared_border,waterway
		FROM country,geography
		WHERE country.geography_id=geography.geography_id
		"""
		)
	countryname=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('geography.html',title="Geographic Details",L=countryname)



@app.route('/states')
def get_states():
	return render_template('states.html',title="List Of States")



@app.route('/states',methods=['POST'])
def state_helper():
	value=request.form["country_name"]
	return redirect('/states/'+str(value))


@app.route('/states/<country_name>')
def get_state_details(country_name):
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"""
		SELECT states.name,states.id,country_name,country.id
		FROM country,states
		WHERE country.id=states.country_id AND country.country_name={}
		""".format('$$'+country_name+'$$')
		)
	countryname=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('state_details.html',title="List Of States",L=countryname)






	
    
@app.route('/cities')
def get_cities():
	return render_template('cities.html',title="List Of Cities")



@app.route('/cities',methods=['POST'])
def city_helper():
	value=request.form["state_name"]
	return redirect('/cities/'+str(value))


@app.route('/cities/<state_name>')
def get_city_details(state_name):
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"""
		SELECT cities.name,cities.id,states.name,states.id,country_name,country.id
		FROM country,states,cities
		WHERE cities.state_id=states.id AND states.country_id=country.id AND states.name={}
		""".format('$$'+state_name+'$$')
		)
	countryname=cur.fetchall()

	cur.close()
	conn.close()
	return render_template('city_details.html',title="List Of Cities",L=countryname)



@app.route('/contribute')
def render_contribute():
	return render_template('contribute.html',title="Enter the data you want to add to the database")


@app.route('/contribute_recv')
def render_contribute_recv():
	return render_template('contribute_recv.html')


@app.route('/contribute',methods=['POST'])
def contribute_helper():
	L=[request.form["city_name"],request.form["state_name"],request.form["country_name"],request.form["city_id"],request.form["state_id"],request.form["country_id"],request.form["state_code"]]
	print(L)
	conn=get_db_connection()
	cur=conn.cursor()
	cur.execute(
		"SELECT * FROM country WHERE country.id={0} AND country.country_name={1}".format(int(L[5]),'$$'+str(L[2])+'$$')
	)
	A1=cur.fetchall()

	cur.execute(
		"SELECT * FROM states WHERE states.id={0} AND states.name={1} AND states.state_code={2}".format(int(L[4]),'$$'+str(L[1])+'$$','$$'+str(L[6])+'$$')
	)
	A2=cur.fetchall()
	cur.execute(
		"SELECT * FROM cities WHERE cities.id={0}".format(int(L[3]))
	)
	A3=cur.fetchall()
	flag=(len(A1)!=0 and len(A2)!=0 and len(A3)==0)
	print(L)
	if(flag):
		cur.execute(
			"""
			INSERT INTO cities(id,name,state_id,country_id) VALUES({0},{1},{2},{3})
			""".format(int(L[3]),'$$'+str(L[0])+'$$',int(L[4]),int(L[5]))
			)
		conn.commit()
	
	return redirect('contribute_recv')









	
app.run()