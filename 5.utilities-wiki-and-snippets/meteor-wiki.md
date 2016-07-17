#### Install Meteor framework and MongoDB at once

~~~~
$ curl https://install.meteor.com/ | sh
~~~~


#### Create and build Meteor project

~~~~
$ meteor create {PROJECT NAME}
$ meteor run
~~~~


#### Check basic CRUD methods

- Run MongoDB console

~~~~
$ meteor mongo
~~~~

- MongoDB native command

~~~~
# Create
mongo > db.tableName.insert(
	{fieldA: 1, fieldB: 'foo'}
);

# Read
mongo > db.tableName.find(
	{fieldA: 1}, 
	{fieldA: 1, fieldB: 1}
);

# Update
mongo > db.tableName.update(
	{fieldA: 1}, 
	{$set: {fieldB: 'foo changed'}},
	{multi: true}
);

# Delete
mongo > db.tableName.remove(
	{fieldA: 1}
);
~~~~

- Meteor's Collection API

~~~~
# Declare Meteor collection
TableName = new Meteor.Collection('tableName');

# Create
TableName.insert(
	{fieldA: 1, fieldB: 'foo'}
);

# Read
TableName.find(
	{fieldA: 1}, 
	{fields: {fieldA: 1, fieldB: 1}}
);

# Update
TableName.update(
	{fieldA: 1},
	{$set: {fieldB: 'foo changed'}},
	{multi: true}
);

# Delete
TableName.remove(
	{fieldA: 1}
);
~~~~


#### Install packages (Find more at atmosperejs.com)

~~~~
$ meteor add {PACKAGE NAME}
~~~~


#### Some helpful packages
  
- accounts-password	*(User account system)*
-	iron:router *(Router)*
-	aldeed:collection2 *(Automatic validation of insert and update)*
-	email	*(Send email)*
-	twbs:bootstrap *(Bootstrap 3)*
-	rajit:bootstrap3-datepicker	*(Bootstrap 3 datepicker)*
-	nemo64:bootstrap *(Configuration for Bootstrap 3)*
-	fourseven:scss *(SASS)*
-	meteorhacks:fast-render *(Render app before DDP connection alive)*
-	force-ssl	*(Force to use SSL)*


#### Remove some insecure packages

~~~~
$ meteor remove autopublish insecure
~~~~


#### Check installed package list

~~~~
$ meteor list
~~~~


#### Set directory structure

- **client** *(Front-end source code like HTML, JS, CSS)*
- **lib** *(Common code for both client and server)*
- **private** *(Resources only accessible from the server side)*
- **public** *(Accessible with root path ('/'). e.g. favicon.ico)*
- **server** *(Back-end source code)*
