angular.module('TestWise')
.controller('AddTestController', function(){
	var self = this;
    self.data = {};
    self.NoOfQuestions = 5;
    console.log("TEST");
    console.log(self.NoOfQuestions);

    self.optionsAvailable= {};
    self.pages = 10 ;
    self.output = [];
    self.range = function(min,max,step)
  	{
  		// console.log("Called");
  		step = step || 1;
  		var input = [];
  		for (var i = min; i <= max; i++)
  		{
  			// console.log(i)
  			input.push(i)
  		}
        self.output.push(input);
  		return input
	};



    self.Range = function(start, end) {
    var result = [];
    for (var i = start; i <= end; i++) {
        result.push(i);
    }
    return result;
    };

    self.optionsAvailable =
    {
        availableOptions:
    	[
            {id: '0', name: 'Text'},
            {id: '1', name: 'Choose One'},
            {id: '2', name: 'Multi-Choice'},
            {id: '3', name: 'Boolean'}
        ]
    }

    self.print = function()
    {
        self.data['test_name'] = self.test_name;
        self.data['course_id'] = self.course_id;
        self.data['questions'] = self.output;
    	console.log(self.data);


        //var qset = [];
        //var qtagset = [];
        //var answerset = [];
        //for(var item in self.values) {
        //    if(self.values.hasOwnProperty(item)) {
        //        if(item.endsWith("question")) {
        //            qset.push(item);
        //        } else if(item.endsWith("question_ta"))
        //    }
        //}

    }

})