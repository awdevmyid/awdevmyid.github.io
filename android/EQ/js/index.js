function createXmlForQuestions() {

    var doc = document.implementation.createDocument("", "", null);
    var quiz = doc.createElement("quiz");

    // Create initial category to make sure we're in the right place.
    // If wildcards are used, we need to order those questions last for processing.
    createCategory(quiz, doc, $('#category').val());

    // Order by if wildcards are used (put last).
    var questionElems = $('#questions').children();
    var noWildcardQuestions = [];
    var wildcardQuestions = [];

    questionElems.each(function () { 
        var qid = $(this).find('.col-md-12').attr('data-qid');
        if (qid === "NUMBER") {
            return;
        }
        var text = $(this).find('#question-text-' + qid).data('editor').getContents();
        // If it has wildcards...
        if (/{.*}/gi.test(text)) {
            wildcardQuestions.push($(this));
        } else {
            noWildcardQuestions.push($(this));
        }
    });

    // Concat the wildcard at the end.
    noWildcardQuestions.concat(wildcardQuestions).forEach(function(elem) { getQuestion(quiz, doc, $(elem)) });

    doc.appendChild(quiz);

    var serializer = new XMLSerializer();
    var xmlString = serializer.serializeToString(doc);

    $('#delete-me').remove();

    var filename = "Moodle EQG Questions.xml";
    var pom = document.createElement('a');
    var bb = new Blob(['<?xml version="1.0" encoding="UTF-8"?>'+xmlString], {type: 'text/plain'});

    pom.setAttribute('href', window.URL.createObjectURL(bb));
    pom.setAttribute('download', filename);
    pom.setAttribute('id', 'delete-me');
    pom.dataset.downloadurl = ['text/plain', pom.download, pom.href].join(':');
    pom.draggable = true; 
    pom.classList.add('dragout');

    pom.click();

    //$('#dump').text('<?xml version="1.0" encoding="UTF-8"?>' + xmlString);
}

function getQuestion(quiz, doc, qElem) {
    // Takes in the XML creator and adds to it for the question.
    var qid = qElem.find('.col-md-12').attr('data-qid');
    if (qid === 'NUMBER') {
        return;
    }

    var name = qElem.find('#question-name-' + qid).val();
    var text = qElem.find('#question-text-' + qid).data('editor').getContents();
    var hasWildcards = /{.*}/gi.test(text);
    var mark = qElem.find('#question-default-mark-' + qid).val();
    var genFeed = qElem.find('#question-general-feedback-' + qid).data('editor').getContents();
    var format = qElem.find('#question-response-format-' + qid).val();
    var reqText = qElem.find('#question-require-text-' + qid).val();
    var boxSize = qElem.find('#question-input-box-' + qid).val();
    var graderInfo = qElem.find('#question-grader-info-' + qid).data('editor').getContents();
    var responseTemplate = qElem.find('#question-response-template-' + qid).data('editor').getContents();

    if (!hasWildcards) {
        createXmlForQuestion(quiz, doc, qid, name, text, mark, genFeed, format, reqText, boxSize, graderInfo, responseTemplate);
    } else {
        var orWildcards = Array.from(text.matchAll(/{.*?[\|].*?}/gi));
        var rangeWildcards = Array.from(text.matchAll(/{[\d-]+}/gi));
        
        var orWildcardsFiltered = [];
        // Filter out duplicate wildcard matches (when a user uses multiple of the same wildcard we treat them as one).
        var matchedVals = [];
        orWildcards.forEach(function (wildcard) {
            // Not present so push to filtered.
            if (matchedVals.indexOf(wildcard[0]) === -1) {
                matchedVals.push(wildcard[0]);
                orWildcardsFiltered.push(wildcard);
            }
        });

        // Create a category for this question, it will not have a single question but many, many questions.
        createCategory(quiz, doc, name + '-' + qid, $('#category').val())
        
        var wildcardValues = [];

        // Process all or wildcards together, adding to the wildcard values array of arrays.
        orWildcardsFiltered.forEach(function (wildcard) {
            var possibleValues = wildcard[0].replace('{', '').replace('}', '').split('|');
            wildcardValues.push(possibleValues);
        });

        console.log(wildcardValues);

        // Boom, generate all combinations possible with the wildcards given for the supplied text.
        var questionsToCreate = generateAllCombinationsOfText(wildcardValues, matchedVals, text);
        console.log(questionsToCreate);

        // Create questions for all.
        questionsToCreate.forEach(function (val, idx) {
            createXmlForQuestion(quiz, doc, qid, name + idx, val, mark, genFeed, format, reqText, boxSize, graderInfo, responseTemplate);
        });

    }
}
function createXmlForQuestion(quiz, doc, qid, name, text, mark, genFeed, format, reqText, boxSize, graderInfo, responseTemplate) {

    console.log(qid, name, text, mark, genFeed, format, reqText, boxSize, graderInfo, responseTemplate);

    var q = doc.createElement('question');
    q.setAttribute('type', 'essay');

    // Question Name.
    var qName = doc.createElement('name');
    createTextElementWithValue(doc, qName, name, false);
    q.appendChild(qName);

    // Question Text.
    var qText = doc.createElement('questiontext');
    qText.setAttribute('format', 'html');
    createTextElementWithValue(doc, qText, text, true);
    q.appendChild(qText);

    // General Feedback.
    var qGeneralFeedback = doc.createElement('generalfeedback');
    qGeneralFeedback.setAttribute('format', 'html');
    createTextElementWithValue(doc, qGeneralFeedback, genFeed, true);
    q.appendChild(qGeneralFeedback);

    // Default Grade
    createTextElementWithValue(doc, q, parseFloat(mark), false, 'defaultgrade');

    // Penalty: unimplemented.
    createTextElementWithValue(doc, q, parseFloat(0), false, 'penalty');
    // Hidden: unimplemented.
    createTextElementWithValue(doc, q, '0', false, 'hidden');
    // ID Number: unimplemented.
    createTextElementWithValue(doc, q, '', false, 'idnumber');
    // Response Format
    createTextElementWithValue(doc, q, format, false, 'responseformat');
    // Response Required
    createTextElementWithValue(doc, q, reqText, false, 'responserequired');
    // Input box size
    createTextElementWithValue(doc, q, boxSize, false, 'responsefieldlines');

    // Attachments: unimplemented.
    var attachments = format === 'editorfilepicker' ? 1 : 0;
    createTextElementWithValue(doc, q, attachments, false, 'attachments');
    // Attachments required: unimplemented.
    createTextElementWithValue(doc, q, '0', false, 'attachmentsrequired');

    // Grader feedback/info.
    var qGraderInfo = doc.createElement('graderinfo');
    qGraderInfo.setAttribute('format', 'html');
    createTextElementWithValue(doc, qGraderInfo, graderInfo, true);
    q.appendChild(qGraderInfo);

    // Response Template.
    var qRespTemplate = doc.createElement('responsetemplate');
    qRespTemplate.setAttribute('format', 'html');
    createTextElementWithValue(doc, qRespTemplate, responseTemplate, true);
    q.appendChild(qRespTemplate);

    quiz.appendChild(q);
}

function createTextElementWithValue(doc, appender, value, isCDATA, elemName) {
    var textNode = doc.createElement(elemName || 'text');
    var v = isCDATA ? doc.createCDATASection(value) : doc.createTextNode(value);
    textNode.appendChild(v);    
    appender.appendChild(textNode);
}

function createCategory(quiz, doc, categoryName, previousCategory) {

    if (previousCategory === undefined) {
        previousCategory = '';
    } else {
        previousCategory += '/';
    }

    var q = doc.createElement('question');
    q.setAttribute('type', 'category');

    var qCat = doc.createElement('category');
    createTextElementWithValue(doc, qCat, '$course$/top/' + previousCategory + categoryName, false);
    q.appendChild(qCat);

    var qInfo = doc.createElement('info');
    qInfo.setAttribute('format', 'html');
    createTextElementWithValue(doc, qInfo, 'Category for ' + previousCategory + categoryName, false);
    q.appendChild(qInfo);

    createTextElementWithValue(doc, q, '', false, 'idnumber');

    quiz.appendChild(q);
}

var kothingEditorOptions = {
    display: "block",
    width: "100%",
    height: "200px",
    popupDisplay: "full",
    toolbarItem: [
      ["undo", "redo"],
      ["formatBlock"],
      [
        "bold",
        "underline",
        "italic",
        "strike",
        "subscript",
        "superscript",
        "fontColor",
        "hiliteColor",
      ],
      ["outdent", "indent", "align", "list", "horizontalRule"],
      ["link", "table", "image"],
      ["lineHeight", "paragraphStyle", "textStyle"],
      ["showBlocks", "codeView"],
      ["preview", "fullScreen"],
      ["removeFormat"],
    ],
    charCounter: true,
};

$(document).ready(function () {

    $('#add-question').click(function () {
        var template = $('#question-template').clone();
        var appendTo = $('#questions');
        var newQuestionNumber = appendTo.children().length;
        template.css('display', 'block');
        template.removeAttr('id');
        template.html(function() { 
            return $(this).html().replace(/NUMBER/g, newQuestionNumber);
        });
        appendTo.append(template);


        $('#question-general-feedback-' + newQuestionNumber).data('editor', 
            KothingEditor.create('question-general-feedback-' + newQuestionNumber, kothingEditorOptions));
        $('#question-grader-info-' + newQuestionNumber).data('editor', 
            KothingEditor.create('question-grader-info-' + newQuestionNumber, kothingEditorOptions));
        $('#question-response-template-' + newQuestionNumber).data('editor', 
            KothingEditor.create('question-response-template-' + newQuestionNumber, kothingEditorOptions));
        $('#question-text-' + newQuestionNumber).data('editor', 
            KothingEditor.create('question-text-' + newQuestionNumber, kothingEditorOptions));

    });

    $('#generate').click(createXmlForQuestions);
});
